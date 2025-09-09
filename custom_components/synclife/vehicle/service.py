from datetime import datetime
from typing import cast

from homeassistant.core import HomeAssistant

from .model import Vehicle, VehicleMileage, VehicleMaintenance
from ..const import DOMAIN, MANAGER, ENTRY_VEHICLES
from ..util.manager import ObjectManager


def get_all() -> [Vehicle]:
    return Vehicle.select()


def get_last_km_by_vehicle(vehicle: Vehicle) -> VehicleMileage | None:
    last_mileage: VehicleMileage = (
        VehicleMileage
        .select()
        .where(VehicleMileage.vehicle == vehicle)
        .order_by(VehicleMileage.created_at.desc())
        .first()
    )
    return last_mileage


async def update_vehicle_maintenances(hass: HomeAssistant) -> None:
    """
    Chamado a cada 12 horas para atualizar os percentuais e reinicia a entry
    """
    manager: ObjectManager = hass.data[DOMAIN][MANAGER]

    for vehicle in get_all():
        vehicle = cast(Vehicle, vehicle)

        current_mileage = 0
        now = datetime.now()

        vehicle_mileage: VehicleMileage = get_last_km_by_vehicle(vehicle)
        if vehicle_mileage is not None:
            current_mileage = vehicle_mileage.mileage

        for maintenance in vehicle.maintenances:
            maintenance = cast(VehicleMaintenance, maintenance)

            percent_mileage = None
            percent_time = None

            # ---- cálculo por quilometragem ----
            if (
                    maintenance.last_mileage is not None
                    and maintenance.next_mileage is not None
                    and maintenance.next_mileage > maintenance.last_mileage
            ):
                delta_total = maintenance.next_mileage - maintenance.last_mileage
                delta_current = current_mileage - maintenance.last_mileage
                percent_mileage = max(0, min(100, (delta_current / delta_total) * 100))

            # ---- cálculo por tempo ----
            if (
                    maintenance.last_date is not None
                    and maintenance.next_date is not None
                    and maintenance.next_date > maintenance.last_date
            ):
                delta_total = (maintenance.next_date - maintenance.last_date).days
                delta_current = (now - maintenance.last_date).days
                if delta_total > 0:
                    percent_time = max(0, min(100, (delta_current / delta_total) * 100))

            # ---- escolhe o maior percentual ----
            candidates = [p for p in [percent_mileage, percent_time] if p is not None]
            percentage = max(candidates) if candidates else None

            # ---- atualiza banco ----
            if percentage is not None:
                maintenance.percentage = round(percentage, 1)
            else:
                maintenance.percentage = None
            maintenance.bool_required = percentage is not None and percentage >= 100
            maintenance.save()

            print(
                f"[{vehicle.name}] {maintenance.type} -> "
                f"KM%={percent_mileage}, DATE%={percent_time}, FINAL={percentage}, "
                f"required={maintenance.bool_required}"
            )

    entry = manager.get_by_key(ENTRY_VEHICLES)
    await hass.config_entries.async_reload(entry.entry_id)
