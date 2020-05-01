# Smart City Scenario

## Scenario
---
IoT-enabled smart city use cases span multiple areas: from contributing to a healthier environment and improving traffic to enhancing public safety and optimizing street lighting.

## Sensors
---
1. Traffic Sensor
Description: This Traffic sensor is deployed at the start and end of each road junction and captures the number of vehicles currently on this particular stretch of road.
Type: One way
Data Generated: This sensor would be giving a value (inflow - outflow), where inflow is between 0-200 and outflow ≤ inflow
Rate: This sensor would be sending values every 90 seconds.
Simulation: 25% inflow values should be within the range 0 to 50
            50% inflow values should be within the range 51 to 125
            15% inflow values should be within the range 126 to 175
            10% inflow values should be within the range 176 to 200
2. Streetlight Sensor
Description: This sensor is deployed at the streetlights between the road junctions. When there is any movement on the road, it generates a stream of bit 1 (ON), otherwise 0  (OFF).
Type: One way
Data Generated: continuously (0 when there is no movement, 1 when there is movement)
Rate: Continuous stream
Simulation: 95% values should be 1
            5% values should be 0
3. Parking Sensor
Description: This sensor is deployed at the parking gate which streams the number of vehicles parked
Type: Two way, should be able to display the availability of parking
Data Generated: This sensor would be giving a number between 0 and 100
Rate: This sensor would be sending values every 300 seconds
Simulation: 10% values should be within the range 0 to 15
            60% values should be within the range 16 to 60
            20% values should be within the range 61 to 90
            10% values should be within the range 91 to 100

## Services / Algorithms
---
1. Traffic monitoring service
This service accepts the output from the Traffic Sensor and checks its range.
    - If the range is between 0 and 50 then it sends a message "LOW_TRAFFIC" + "value of sensor"
    - If the range is between 51 and 125 then it sends a message "MODERATE_TRAFFIC" + "value of sensor"
    - If the range is between 126 and 175 then it sends a message "HIGH_TRAFFIC" + "value of sensor"
    - If the range is between 176 and 200 then it sends a message "CONGESTION" + "value of sensor"

    Also shows a graph of the traffic in last 24 hours.
2. Streetlight scheduling service
This service runs between sunset_time and sunrise_time
3. Parking availability service
This service accepts the output from the Parking Sensor and checks its range.
    - If the range is between 0 and 60 then it sends a message "HIGH AVAILIBILITY" + "value of sensor"
    - If the range is between 61 and 90 then it sends a message "FILLING FAST" + "value of sensor"
    - If the range is between 91 and 99 then it sends a message "ALMOST FILLED" + "value of sensor"
    - If the value is 100 then sends a message "FILLED" + "value of sensor"

## User Interface
---

## Flow
---

## Testing
---
