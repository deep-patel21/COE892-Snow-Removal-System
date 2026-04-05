import grpc
import time
from concurrent import futures

#import the proto code
import snow_removal_pb2
import snow_removal_pb2_grpc

import data_utilities as utils

#This server recieves coordinates, it then fetches the data from the APIs in data_extraction.py,
#as well as sending data back to the Scheduler
class RoadMonitorService(snow_removal_pb2_grpc.RoadMonitorServicer):
    def StreamConditions(self, request, context):
        print(f"Stream initiated for: {request.latitude}, {request.longitude}")
        
        #In a normal environment this would be a while true loop, however I don't have enough 
        #credits left for the APIs, for that, so for now just simulate sending 5 payloads
        for i in range(5):
            if not context.is_active():
                print("Client disconnected. Terminating stream.")
                break
                
            #fetch the data
            traffic = utils.fetch_traffic_data(request.latitude, request.longitude)
            weather = utils.fetch_weather_data(request.latitude, request.longitude)
            
            #FRC categorizations, FRC0/1/2 is for highways, file FRC3/4 is or main street, anything else is residential
            road_type = utils.calculate_road_type(traffic["frc"])

            #higher snow fall = higher priority
            priority_level =  utils.calculate_priority_level(weather["snow_depth_mm"])

            #package it into the WeatherData structure
            weather_msg = snow_removal_pb2.WeatherData(
                temperature_c=weather["temperature_c"],
                wind_speed_kmh=weather["wind_speed_kmh"],
                snow_depth_mm=weather["snow_depth_mm"]
            )
            
            #yield the final RoadCondition payload
            yield snow_removal_pb2.RoadConditionUpdate(
                road_type=road_type,
                dispatch_priority=priority_level,
                traffic_speed_kmh=traffic["current_speed"],
                weather=weather_msg
            )
            
            print(f"Update {i+1} sent to client.")
            
            # Pause to respect API rate limits and simulate real-time monitoring
            time.sleep(10)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    snow_removal_pb2_grpc.add_RoadMonitorServicer_to_server(RoadMonitorService(), server)
    
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Extraction Module gRPC Server is active on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()