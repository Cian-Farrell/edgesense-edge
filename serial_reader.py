import serial
import time
import json
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder

# Serial config
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

# AWS IoT config
ENDPOINT = "a3ukfj6l4dra4j-ats.iot.eu-west-1.amazonaws.com"
CLIENT_ID = "edgesense-raspberry-pi"
TOPIC = "edgesense/sensor-data"
CERT_PATH = r"C:\Users\cianf\InternalPlacement\certs\86f52f8b5a613ca70021e08a299db7a2a110aeb70eef4239b4615a4ab88befd6-certificate.pem.crt"
KEY_PATH = r"C:\Users\cianf\InternalPlacement\certs\86f52f8b5a613ca70021e08a299db7a2a110aeb70eef4239b4615a4ab88befd6-private.pem.key"
CA_PATH = r"C:\Users\cianf\InternalPlacement\certs\AmazonRootCA1.pem"

def connect_mqtt():
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=CERT_PATH,
        pri_key_filepath=KEY_PATH,
        client_bootstrap=client_bootstrap,
        ca_filepath=CA_PATH,
        client_id=CLIENT_ID,
        clean_session=False,
        keep_alive_secs=30
    )

    print("Connecting to AWS IoT Core...")
    connect_future = mqtt_connection.connect()
    connect_future.result()
    print("Connected!")
    return mqtt_connection

def read_serial(mqtt_connection):
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Reading from Arduino on {SERIAL_PORT}")

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            temp, humidity = line.split(',')

            payload = json.dumps({
                "temperature": float(temp),
                "humidity": float(humidity),
                "timestamp": time.time()
            })

            mqtt_connection.publish(
                topic=TOPIC,
                payload=payload,
                qos=mqtt.QoS.AT_LEAST_ONCE
            )
            print(f"Published: {payload}")

        time.sleep(0.1)

if __name__ == "__main__":
    mqtt_connection = connect_mqtt()
    read_serial(mqtt_connection)