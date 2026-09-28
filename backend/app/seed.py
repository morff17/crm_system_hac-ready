from datetime import date
from sqlalchemy.orm import Session
from .models import Manager, Direction, Product, Institution, InstitutionContact, Workflow, WorkflowStage, Interaction, InteractionEvent

STAGES = [
    "Поиск контактов ответственного в вузе",
    "Коммуникация и уточнение актуальности программ",
    "Организация встречи",
    "Обмен пакетом документов",
    "Корректировка документов",
    "Подписание документов",
    "Передача материалов, лицензии и документации",
    "Сопровождение внедрения ИТ-продуктов",
    "Обучение преподавателей",
    "Актуализация учебной программы",
    "Ведение занятий",
    "Актуализация документации и материалов",
    "Повышение квалификации преподавателей",
    "Контроль исполнения этапов",
]

def seed(db: Session):
    if db.query(Institution).count():
        return
    managers = [
        Manager(full_name="Иванова Анна Алексеевна", email="ivanova.a@rt.ru", phone="+7 (495) 123-45-67", keycloak_username="user"),
        Manager(full_name="Смирнова Елена Олеговна", email="smirnova.e@rt.ru"),
        Manager(full_name="Петров Алексей Владимирович", email="petrov.a@rt.ru"),
    ]
    db.add_all(managers); db.flush()
    directions = [Direction(name=n) for n in ["DevOps", "QA", "Data Science", "Кибербезопасность", "Разработка ПО"]]
    db.add_all(directions); db.flush()
    products = [
        Product(name="Deckhouse", vendor="Флант", direction=directions[0]),
        Product(name="GitLab", vendor="GitLab", direction=directions[4]),
        Product(name="PostgreSQL", vendor="Postgres Professional", direction=directions[2]),
        Product(name="Security Code", vendor="Код Безопасности", direction=directions[3]),
    ]
    db.add_all(products); db.flush()
    workflow = Workflow(name="Базовый workflow РТК")
    db.add(workflow); db.flush()
    stages = [WorkflowStage(workflow_id=workflow.id, name=n, position=i + 1) for i, n in enumerate(STAGES)]
    db.add_all(stages); db.flush()
    data = [
        ("МГТУ им. Баумана", "Москва", "Москва", "Активный", "РТК-025-001", managers[0]),
        ("СПбПУ", "Санкт-Петербург", "Санкт-Петербург", "В процессе", "РТК-025-014", managers[1]),
        ("КФУ", "Республика Татарстан", "Казань", "Активный", "РТК-025-022", managers[2]),
        ("НИУ ВШЭ", "Москва", "Москва", "Активный", "РТК-026-003", managers[0]),
        ("УрФУ", "Свердловская область", "Екатеринбург", "Планируется", None, managers[1]),
        ("НГТУ", "Новосибирская область", "Новосибирск", "Активный", "РТК-025-037", managers[2]),
        ("ЮУрГУ", "Челябинская область", "Челябинск", "В процессе", "РТК-026-010", managers[0]),
        ("ДВФУ", "Приморский край", "Владивосток", "Активный", "РТК-025-051", managers[1]),
    ]
    for i, (name, region, city, status, contract, manager) in enumerate(data):
        inst = Institution(
            name=name, short_name=name, full_name=name, region=region, city=city,
            institution_type="ВУЗ", site="example.edu.ru", description="Учебное заведение — участник программы ИТ Школы РТК.",
            status=status, vendor=products[i % len(products)].vendor, software=products[i % len(products)].name,
            contract_number=contract, license_signed=date(2026, 1, 15) if contract else None,
            license_until=date(2027, 12, 31) if contract else None,
            transfer_status="Передано" if status == "Активный" else "В работе", manager=manager,
            comment="Данные демонстрационного контура."
        )
        db.add(inst); db.flush()
        db.add(InstitutionContact(institution_id=inst.id, full_name="Смирнов Евгений Олегович", position="Проректор по цифровому развитию", email="contact@example.edu.ru"))
        current = stages[min(i + 3, len(stages)-1)]
        interaction = Interaction(
            institution_id=inst.id, direction_id=directions[i % len(directions)].id, product_id=products[i % len(products)].id,
            workflow_id=workflow.id, current_stage_id=current.id, status=status,
            students_count=120 + i * 35, streams_count=1 + i % 3, applications_count=150 + i * 40,
            started_at=date(2026, 1 + (i % 6), 1)
        )
        db.add(interaction); db.flush()
        db.add(InteractionEvent(interaction_id=interaction.id, to_stage_id=current.id, comment="Начальный импорт", author="seed"))
    db.commit()
