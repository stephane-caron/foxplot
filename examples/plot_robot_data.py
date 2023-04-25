from foxplot import Fox

if __name__ == "__main__":
    fox = Fox(from_file="robot_data.json", time="time")
    action = fox.data.action
    observation = fox.data.observation
    fox.plot(
        left=[
            action.wheel_balancer.ground_velocity,
            observation.wheel_odometry.velocity,
        ],
        right=[observation.servo.left_wheel.velocity],
    )
