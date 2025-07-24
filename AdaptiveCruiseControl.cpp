#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <thread>

// Constants and Parameters for ACC
const double MAX_SPEED = 150.0;            // km/h
const double MIN_FOLLOW_DISTANCE = 5.0;    // meters
const double MAX_ACCELERATION = 3.0;       // m/s^2
const double MAX_DECELERATION = -5.0;      // m/s^2
const double TIME_GAP = 1.5;                // seconds between vehicles

// Enum for Cruise Control State
enum class ACCState {
    OFF,
    STANDBY,
    ACTIVE,
    ERROR
};

// Simulated sensor data representing a leading vehicle
struct LeadVehicle {
    double distance;   // meters to lead vehicle
    double speed;      // km/h
    bool detected;
};

class AdaptiveCruiseControl {
private:
    ACCState state;
    double currentSpeed;      // km/h
    double desiredSpeed;      // km/h
    double accelCommand;      // m/s^2
    LeadVehicle leadVehicle;

public:
    AdaptiveCruiseControl() : state(ACCState::OFF), currentSpeed(0.0), desiredSpeed(0.0), accelCommand(0.0) {
        leadVehicle = {0.0, 0.0, false};
    }

    // Initializes the ACC system and puts it in standby mode
    void initialize(double initialSpeed) {
        currentSpeed = initialSpeed;
        desiredSpeed = initialSpeed;
        accelCommand = 0.0;
        state = ACCState::STANDBY;
        std::cout << "ACC Initialized and in STANDBY mode." << std::endl;
    }

    // Sets the desired cruise speed
    void setDesiredSpeed(double speed) {
        if (speed > 0 && speed <= MAX_SPEED) {
            desiredSpeed = speed;
            std::cout << "Desired speed set to " << desiredSpeed << " km/h." << std::endl;
        } else {
            std::cerr << "Invalid desired speed value." << std::endl;
            state = ACCState::ERROR;
        }
    }

    // Processes lead vehicle sensor data (distance in meters, speed in km/h, and detection status)
    void updateLeadVehicle(double distance, double speed, bool detected) {
        leadVehicle.distance = distance;
        leadVehicle.speed = speed;
        leadVehicle.detected = detected;
    }

    // Calculates safe following distance based on current speed and time gap
    double calculateSafeDistance() const {
        // Convert speed km/h to m/s
        double speed_m_s = currentSpeed / 3.6;
        return std::max(MIN_FOLLOW_DISTANCE, speed_m_s * TIME_GAP);
    }

    // Updates the acceleration command based on current conditions
    void updateAccelerationCommand() {
        if (state == ACCState::ERROR) {
            accelCommand = 0.0;
            return;
        }

        if (leadVehicle.detected) {
            double safeDistance = calculateSafeDistance();

            if (leadVehicle.distance < safeDistance) {
                // Too close to lead vehicle, decelerate aggressively
                accelCommand = MAX_DECELERATION;
            } else if (leadVehicle.distance < safeDistance + 10) {
                // Adjust speed to maintain safe distance
                double relativeSpeed = (leadVehicle.speed - currentSpeed) / 3.6;  // m/s
                accelCommand = std::max(MAX_DECELERATION, std::min(MAX_ACCELERATION, relativeSpeed));
            } else {
                // Lead vehicle far away, try to reach desired speed gradually
                if (currentSpeed < desiredSpeed) {
                    accelCommand = MAX_ACCELERATION / 2;
                } else if (currentSpeed > desiredSpeed) {
                    accelCommand = MAX_DECELERATION / 2;
                } else {
                    accelCommand = 0.0;
                }
            }
        } else {
            // No lead vehicle detected, maintain desired speed
            if (currentSpeed < desiredSpeed) {
                accelCommand = MAX_ACCELERATION / 2;
            } else if (currentSpeed > desiredSpeed) {
                accelCommand = MAX_DECELERATION / 2;
            } else {
                accelCommand = 0.0;
            }
        }
    }

    // Updates the current speed based on the acceleration command and time step
    void updateSpeed(double deltaTime) {
        // Convert current speed to m/s
        double speed_m_s = currentSpeed / 3.6;

        // Update speed with acceleration command (m/s^2) over deltaTime seconds
        speed_m_s += accelCommand * deltaTime;

        // Clamp speed within safe range
        speed_m_s = std::max(0.0, speed_m_s);

        // Update currentSpeed in km/h
        currentSpeed = speed_m_s * 3.6;

        // Clamp currentSpeed to MAX_SPEED
        if (currentSpeed > MAX_SPEED) {
            currentSpeed = MAX_SPEED;
        }
    }

    // Starts ACC system (active mode)
    void start() {
        if (state == ACCState::STANDBY) {
            state = ACCState::ACTIVE;
            std::cout << "ACC Activated." << std::endl;
        } else {
            std::cerr << "ACC can only start from STANDBY state." << std::endl;
        }
    }

    // Stops ACC system and returns to STANDBY
    void stop() {
        if (state == ACCState::ACTIVE) {
            state = ACCState::STANDBY;
            accelCommand = 0.0;
            std::cout << "ACC Deactivated, back to STANDBY." << std::endl;
        }
    }

    // Returns current system state as string
    std::string getStateString() const {
        switch (state) {
            case ACCState::OFF:
                return "OFF";
            case ACCState::STANDBY:
                return "STANDBY";
            case ACCState::ACTIVE:
                return "ACTIVE";
            case ACCState::ERROR:
                return "ERROR";
            default:
                return "UNKNOWN";
        }
    }

    // Main periodic update function: updates ACC logic every cycle
    void update(double deltaTime, const LeadVehicle& sensorData) {
        updateLeadVehicle(sensorData.distance, sensorData.speed, sensorData.detected);
        updateAccelerationCommand();
        updateSpeed(deltaTime);
    }

    // Prints current status
    void printStatus() const {
        std::cout << "ACC State: " << getStateString() << std::endl;
        std::cout << "Current Speed: " << currentSpeed << " km/h" << std::endl;
        std::cout << "Desired Speed: " << desiredSpeed << " km/h" << std::endl;
        std::cout << "Lead Vehicle: "
                  << (leadVehicle.detected ? "Detected" : "Not Detected")
                  << ", Distance: " << leadVehicle.distance << " m"
                  << ", Speed: " << leadVehicle.speed << " km/h" << std::endl;
        std::cout << "Acceleration Command: " << accelCommand << " m/s^2" << std::endl;
    }
};

// Simulated test loop for ACC module
int main() {
    AdaptiveCruiseControl acc;
    acc.initialize(80.0);    // initial speed 80 km/h
    acc.setDesiredSpeed(100.0);
    acc.start();

    // Simulated lead vehicle pattern
    std::vector<LeadVehicle> leadVehicleData = {
        {50.0, 90.0, true},
        {40.0, 85.0, true},
        {30.0, 80.0, true},
        {20.0, 70.0, true},
        {10.0, 60.0, true},
        {5.0, 50.0, true},
        {0.0, 0.0, false},  // lead vehicle lost
        {0.0, 0.0, false},
        {55.0, 110.0, true},
        {60.0, 115.0, true},
    };

    double deltaTime = 0.1; // seconds
    for (auto& sensorData : leadVehicleData) {
        acc.update(deltaTime, sensorData);
        acc.printStatus();
        std::cout << "---------------------------------------" << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    acc.stop();
    return 0;
}