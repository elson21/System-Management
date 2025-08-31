from app.db.session import SessionLocal
from app.db.db_models import System, Organization
from app.db.db_models.system import SystemStatus

def add_systems():
    with SessionLocal() as db:
        organization = db.query(Organization).first()
        if not organization:
            print("Create an organization.")
            return
        
        systems = [
            {"name": "BESS-001", "status": SystemStatus.FREE},
            {"name": "BESS-002", "status": SystemStatus.CHARGING},
            {"name": "BESS-003", "status": SystemStatus.FREE},
            {"name": "BESS-004", "status": SystemStatus.MAINTENANCE},
            {"name": "BESS-005", "status": SystemStatus.ISLANDING},
            {"name": "BESS-006", "status": SystemStatus.PEAKSHAVING},
            {"name": "BESS-007", "status": SystemStatus.OFFLINE},
            {"name": "BESS-008", "status": SystemStatus.PEAKSHAVING},
            {"name": "BESS-009", "status": SystemStatus.ISLANDING},
            {"name": "BESS-010", "status": SystemStatus.OFFLINE},
        ]

        system_count = 0

        for system in systems:
            system = System(
                name = system["name"],
                status = system["status"],
                organization_id = organization.id
            )

            db.add(system)
            system_count += 1

        print(f"Added {system_count} systems")

        db.commit()

if __name__ == "__main__":
    add_systems()