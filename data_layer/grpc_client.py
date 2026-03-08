"""
Written as a tester file to test gRPC communications
"""

import grpc

import snow_removal_pb2
import snow_removal_pb2_grpc

def run():
    # Establish a connection to the gRPC server
    print("Attempting to connect to the Extraction Module...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = snow_removal_pb2_grpc.RoadMonitorStub(channel)
        
        # Define a test coordinate within your Toronto boundary (Downtown)
        request = snow_removal_pb2.CoordinateRequest(
            latitude=43.6532, 
            longitude=-79.3832
        )
        
        print(f"Requesting conditions for coordinate: {request.latitude}, {request.longitude}\n")
        
        try:
            # Initiate the Server-Side Stream and iterate over incoming messages
            responses = stub.StreamConditions(request)
            for response in responses:
                print("--- LIVE UPDATE RECEIVED ---")
                print(f"Road Type: {response.road_type}")
                print(f"Dispatch Priority: {response.dispatch_priority}")
                print(f"Traffic Speed: {response.traffic_speed_kmh} km/h")
                print(f"Temperature: {response.weather.temperature_c} °C")
                print(f"Snow Depth: {response.weather.snow_depth_cm} cm")
                print(f"Wind Speed: {response.weather.wind_speed_kmh} km/h\n")
        except grpc.RpcError as e:
            print(f"Connection failed or terminated: {e.details()}")

if __name__ == '__main__':
    run()