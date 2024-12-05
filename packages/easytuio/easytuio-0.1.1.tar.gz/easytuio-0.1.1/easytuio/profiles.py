from dataclasses import dataclass, asdict


class TUIOProfile:
    """Base class for TUIO profiles."""
    @classmethod
    def from_osc(cls, args):
        raise NotImplementedError("Subclasses must implement this method.")

    def to_dict(self):
        return asdict(self)

    def __repr__(self):
        return str(self.to_dict())


@dataclass
class TUIO2DCursor(TUIOProfile):
    session_id: int
    x: float
    y: float
    x_vel: float = 0.0
    y_vel: float = 0.0
    motion_acc: float = 0.0

    @classmethod
    def from_osc(cls, args):
        if len(args) < 6:
            raise ValueError(f"Invalid arguments for TUIO2DCursor: {args}")
        return cls(*args)


@dataclass
class TUIO2DObject(TUIOProfile):
    """
    Represents a 2D object profile (e.g., tangible objects).
    """
    session_id: int
    class_id: int
    x: float
    y: float
    angle: float
    x_vel: float = 0.0
    y_vel: float = 0.0
    rot_vel: float = 0.0
    motion_acc: float = 0.0
    rot_acc: float = 0.0

    @classmethod
    def from_osc(cls, args):
        if len(args) < 10:
            raise ValueError(f"Invalid arguments for TUIO2DObject: {args}")
        return cls(
            session_id=args[0],
            class_id=args[1],
            x=args[2],
            y=args[3],
            angle=args[4],
            x_vel=args[5],
            y_vel=args[6],
            rot_vel=args[7],
            motion_acc=args[8],
            rot_acc=args[9],
        )


@dataclass
class TUIO2DBlob(TUIOProfile):
    session_id: int
    x: float
    y: float
    angle: float
    width: float
    height: float
    area: float

    @classmethod
    def from_osc(cls, args):
        if len(args) < 7:
            raise ValueError(f"Invalid arguments for TUIO2DBlob: {args}")
        return cls(*args)
