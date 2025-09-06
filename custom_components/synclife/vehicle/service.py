from .model import Vehicle, VehicleMileage


def get_all() -> [Vehicle]:
    return Vehicle.select()


def get_last_km_by_vehicle(vehicle: Vehicle) -> int | None:
    last_mileage: VehicleMileage = (
        VehicleMileage
        .select()
        .where(VehicleMileage.vehicle == vehicle)
        .order_by(VehicleMileage.created_at.desc())
        .first()
    )
    if last_mileage:
        return last_mileage.mileage
    return None
