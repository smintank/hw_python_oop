from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Training information message."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {}; '
                    'Длительность: {:.3f} ч.; '
                    'Дистанция: {:.3f} км; '
                    'Ср. скорость: {:.3f} км/ч; '
                    'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        """Get info message about training."""

        return self.message.format(self.training_type, self.duration,
                                   self.distance, self.speed, self.calories)


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

        distance: float = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Get spent calories amount."""

        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Return an info message about the completed training."""

        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Training: running."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: int = 1.79

    def get_spent_calories(self) -> float:
        """Get amount of spent calories for running."""

        mean_speed: float = self.get_mean_speed()
        duration_in_minutes: float = self.duration * self.MIN_IN_HOUR
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * duration_in_minutes)


class SportsWalking(Training):
    """Training: sport walking."""

    KMH_IN_MS: float = 0.278
    SPEED_HEIGHT_SHIFT: float = 0.035
    SPEED_HEIGHT_MULTIPLIER: float = 0.029
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

        mean_speed_in_ms: float = self.get_mean_speed() * self.KMH_IN_MS
        duration_in_minutes: float = self.duration * self.MIN_IN_HOUR
        height_in_m: float = self.height / self.CM_IN_M

        return (self.weight * duration_in_minutes
                * (self.SPEED_HEIGHT_SHIFT + self.SPEED_HEIGHT_MULTIPLIER
                   * (mean_speed_in_ms ** 2 / height_in_m)))


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

    training_types: list[str: Training] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in training_types:
        return training_types[workout_type](*data)


def main(training: Training) -> None:
    """Main function."""

    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        if training is not None:
            main(training)
        else:
            print('Передан неизвестный тип тренировки.')
