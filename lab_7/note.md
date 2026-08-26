# Eventarc และ Cloud Run Functions

## Eventarc
- **แผนกรับเรื่องและกระจายข่าว** (Broadcaster/Router)
- ตัวมัน **ไม่ประมวลผล Business Logic** เอง
- มีหน้าที่ดักฟังเหตุการณ์จากบริการต่างๆ ใน Google Cloud (มากกว่า 90 บริการ)
- เมื่อเกิดเหตุการณ์ขึ้น:
    - แพ็กข้อมูลในรูปแบบมาตรฐาน (CloudEvents)
    - ส่งต่อข้อมูลไปยังปลายทางทันที

## Cloud Run Functions
- **คนทำงาน** (Worker)
- มีหน้าที่ประมวลผลข้อมูล (เขียนโค้ด เช่น Python, Node.js ฯลฯ)
- สามารถดักฟัง Event พื้นฐานได้ (เช่น Event จาก GCS หรือ Pub/Sub แบบ direct)

### การทำงานร่วมกับ Eventarc
- Cloud Run Functions **ไม่ต้องดักฟัง Event เอง**
- Eventarc จะส่ง HTTP มาปลุกให้ Cloud Run Functions ทำงาน
