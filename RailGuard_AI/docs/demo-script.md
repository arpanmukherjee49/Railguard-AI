# Demo Script

RailGuard AI is an IoT and machine-learning-based predictive maintenance prototype for electric train traction-motor bearings.

We monitor temperature, vibration-related acceleration, motor current and load. In the physical prototype, sensors connect to an ESP32 and the data is transmitted through Wi-Fi using MQTT.

The Python analytics layer receives sensor parameters and the Random Forest model classifies the bearing condition as Normal, Degrading or Fault.

For the online demonstration, the dashboard runs in Demo Mode using simulated values and deliberately moves from normal operation to degradation and finally to fault so the predictive-maintenance workflow is easy to demonstrate.

**Why ML?** Because bearing behaviour depends on multiple operating parameters; the model considers their combined pattern rather than relying only on a single fixed threshold.

**Dataset note:** the prototype uses synthetic training data because a real labelled railway bearing dataset was not available for the hackathon.
