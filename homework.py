class InfoMessage:
    """Training information message."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Training base class."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.weight = weight
        self.duration = duration
        self.action = action

    def get_distance(self) -> float:
        """Get distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get average moving speed."""
        distance = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Get spent calories amount."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Return an info message about the completed training."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Training: running."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Get amount of spent calories for running."""
        mean_speed = self.get_mean_speed()
        duration_in_minutes = self.duration * self.MIN_IN_HOUR
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * duration_in_minutes)


class SportsWalking(Training):
    """Training: sport walking."""

    KMH_IN_MS: float = 0.278
    WEIGHT_COEFFICIENT_1: float = 0.035
    WEIGHT_COEFFICIENT_2: float = 0.029
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Get amount of spent calories for sport walking."""
        mean_speed_in_ms = self.get_mean_speed() * self.KMH_IN_MS
        duration_in_minutes = self.duration * self.MIN_IN_HOUR
        height_in_m = self.height / self.CM_IN_M

        return ((self.WEIGHT_COEFFICIENT_1 * self.weight
                + (mean_speed_in_ms ** 2 / height_in_m)
                * self.WEIGHT_COEFFICIENT_2 * self.weight)
                * duration_in_minutes)


class Swimming(Training):
    """Training: swimming."""

    LEN_STEP: float = 1.38
    SPEED_MODIFIER: float = 1.1
    MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        """Get amount of spent calories for swimming."""
        return ((self.get_mean_speed() + self.SPEED_MODIFIER)
                * self.MULTIPLIER * self.weight * self.duration)

    def get_mean_speed(self) -> float:
        """Get average swimming speed."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Read data received from sensors."""
    training_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Main function."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
