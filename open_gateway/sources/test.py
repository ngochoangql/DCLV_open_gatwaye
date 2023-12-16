import json
import struct
import math
import time
import random
import paho.mqtt.client as mqtt
from open_gateway.sources.base import (
    BaseReader,
    BaseResultReaderMixin,
    BaseStreamReaderMixin,
)


class TestReader(BaseReader):
    name = "TEST"

    def list_available_devices(self):
        return [
            {"id": 1, "name": "M5 Stack", "device_id": "M5 Stack Core 2"},
            {"id": 2, "name": "Test Audio", "device_id": "Test Audio"},
            {
                "id": 3,
                "name": "Test IMU 6-axis Float",
                "device_id": "Test IMU 6-axis Float",
            },
            {"id": 4, "name": "Test Acc", "device_id": "Test IMU 3-axis"},
            {"id": 5, "name": " Test IMU 9-axis", "device_id": "Test IMU 9-axis float"},
        ]


class TestStreamReader(TestReader, BaseStreamReaderMixin):
    @property
    def delay(self):
        return 1.0 / self.sample_rate * self.samples_per_packet / 1.25

    @property
    def byteSize(self):
        if self.config_columns:
            return (
                self.source_samples_per_packet
                * len(self.config_columns)
                * self.data_byte_size
            )

        return 0

    

    def read_device_config(self):

        config = get_test_device_configs(self.device_id)

        self._validate_config(config)

        return config

    def _read_source(self):
        print("Starting to read source test")
        index = 0

        

        self.streaming = True

        if self.run_sml_model:
            sml = self.get_sml_model_obj()
        else:
            sml = None
      
       
        # Thiết lập thông tin MQTT broker và topic
        mqtt_broker_address = "192.168.50.133"
        mqtt_topic = "data"
        global mqtt_data
        mqtt_data = None
        # Hàm xử lý khi nhận được tin nhắn từ MQTT server
        def on_message(client, userdata, message):
            payload = message.payload.decode("utf-8")
            global mqtt_data
            try:
                # Giả sử dữ liệu từ MQTT được định dạng dưới dạng JSON
                mqtt_data = payload
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")
            
        # Khởi tạo MQTT client
        client = mqtt.Client()
        client.on_message = on_message
        # Kết nối đến MQTT broker và đăng ký theo dõi topic
        client.connect(mqtt_broker_address, 1883, 60)
        client.subscribe(mqtt_topic)
        client.loop_start()
        # B client.loop_start()ắt đầu lắng nghe tin nhắn
        
        sleep_time = self.source_samples_per_packet / float(self.sample_rate)
        # data, data_len = self._generate_samples(
        #     len(self.config_columns), self.sample_rate,mqtt_data
        # )
        
        while self.streaming:
            incycle = time.time()

            
            
            
            try:
                
                print("============================")
                print("data_mqtt",mqtt_data)
                if mqtt_data != None :
                    try:
                        data = eval(mqtt_data)
                        format_string = 'f' * len(data)

                        # Sử dụng struct.pack để chuyển tuple thành chuỗi bytes
                        sample_data = bytearray(struct.pack(format_string, *data))
                        

                        # Chuyển mỗi đoạn thành một số nguyên
                        # integer_list = [int(segment,16) for segment in segments]
                        # sample_data =bytearray(integer_list)
                        # print(sample_data)
                        self.buffer.update_buffer(sample_data)
                        # print(sample_data)
                        if self.run_sml_model:
                            self.execute_run_sml_model(sml, sample_data)
                        mqtt_data = None
                    except:
                        time.sleep(0.0001)
            except Exception as e:
                self.disconnect()
                raise e

            incycle = time.time() - incycle

            time.sleep(sleep_time - incycle)


class TestResultReader(TestReader, BaseResultReaderMixin):
    def set_app_config(self, config):
        config["DATA_SOURCE"] = self.name
        config["DEVICE_ID"] = self.device_id

    def _read_source(self):

        self.streaming = True
        if self.run_sml_model:
            sml = self.get_sml_model_obj()
        else:
            sml = None
        
        # Thiết lập thông tin MQTT broker và topic
        mqtt_broker_address = "192.168.50.133"
        mqtt_topic = "data"
        global mqtt_data
        mqtt_data = None
        # Hàm xử lý khi nhận được tin nhắn từ MQTT server
        def on_message(client, userdata, message):
            payload = message.payload.decode("utf-8")
            global mqtt_data
            try:
                # Giả sử dữ liệu từ MQTT được định dạng dưới dạng JSON
                mqtt_data = payload
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON data: {e}")
            
        # Khởi tạo MQTT client
        client = mqtt.Client()
        client.on_message = on_message
        # Kết nối đến MQTT broker và đăng ký theo dõi topic
        client.connect(mqtt_broker_address, 1883, 60)
        client.subscribe(mqtt_topic)
        client.loop_start()
        # B client.loop_start()ắt đầu lắng nghe tin nhắn
        
        # sleep_time = self.source_samples_per_packet / float(self.sample_rate)
        # data, data_len = self._generate_samples(
        #     len(self.config_columns), self.sample_rate,mqtt_data
        # )
        while self.streaming:
            incycle = time.time()
            import random

            # result = json.dumps(
            #     {"ModelNumber": 0, "Classification": random.randint(0, 3)}
            # )
            # self.rbuffer.update_buffer([result, result])
            try:
                
                print("============================")
                print("data_mqtt",mqtt_data)
                if mqtt_data != None :
                    try:
                        data = eval(mqtt_data)
                        format_string = 'f' * len(data)

                        # Sử dụng struct.pack để chuyển tuple thành chuỗi bytes
                        sample_data = bytearray(struct.pack(format_string, *data))
                        

                        # Chuyển mỗi đoạn thành một số nguyên
                        # integer_list = [int(segment,16) for segment in segments]
                        # sample_data =bytearray(integer_list)
                        # print(sample_data)
                        # self.buffer.update_buffer(sample_data)
                        # print(sample_data)
                        if self.run_sml_model:
                            ret = self.execute_run_sml_model_recognition(sml, sample_data)
                            result = json.dumps(
                                {"ModelNumber": 0, "Classification": ret}
                            )
   
                            self.rbuffer.update_buffer([result, result])
                        mqtt_data = None
                    except:
                        time.sleep(0.0001)
            except Exception as e:
                self.disconnect()
                raise e
            # Randomly removes a character to simulate dropped packets
            # index = random.randint(0, len(result) - 1)
            # result = result[:index] + result[index + 1 :]
            
            time.sleep(1)
            
            # incycle = time.time() - incycle

            # time.sleep(sleep_time - incycle)


def get_test_device_configs(device_id):

    config = {}

    if device_id == "Test IMU 6-axis Float":
        config["column_location"] = {
            "AccelerometerX": 0,
            "AccelerometerY": 1,
            "AccelerometerZ": 2,
            "GyroscopeX": 3,
            "GyroscopeY": 4,
            "GyroscopeZ": 5,
        }
        config["sample_rate"] = 119
        config["samples_per_packet"] = 6
        config["data_type"] = "float"

    elif device_id == "Test IMU 6-axis":
        config["column_location"] = {
            "AccelerometerX": 0,
            "AccelerometerY": 1,
            "AccelerometerZ": 2,
            "GyroscopeX": 3,
            "GyroscopeY": 4,
            "GyroscopeZ": 5,
        }

        config["sample_rate"] = 119
        config["samples_per_packet"] = 6
        config["data_type"] = "int16"

    elif device_id == "M5 Stack Core 2":
        config["column_location"] = {
            "Current": 0,
            "ActivePower": 1,
            "ApparentPower":2,
        }
        config["sample_rate"] = 1
        config["samples_per_packet"] = 4
        config["data_type"] = "float"

    elif device_id == "Test Audio":
        config["column_location"] = {"Microphone": 0}
        config["sample_rate"] = 4
        config["samples_per_packet"] = 4

    elif device_id == "Test IMU 9-axis float":
        config["column_location"] = {
            "AccelerometerX": 0,
            "AccelerometerY": 1,
            "AccelerometerZ": 2,
            "GyroscopeX": 3,
            "GyroscopeY": 4,
            "GyroscopeZ": 5,
            "X": 6,
            "Y": 7,
            "Z": 8,
        }
        config["sample_rate"] = 119
        config["samples_per_packet"] = 6
        config["data_type"] = "float"

    else:
        raise Exception("Invalid Device ID")

    return config


if __name__ == "__main__":
    config = {
        "CONFIG_SAMPLES_PER_PACKET": 10,
        "CONFIG_SAMPLE_RATE": 100,
        "CONFIG_COLUMNS": ["X", "Y", "Z"],
    }
    t = TestReader(config, "Test IMU 6-axis")

    t.set_config(config)

    t.connect()

    t.record_start("tester")

    time.sleep(5)

    t.record_stop()

    t.disconnect()
