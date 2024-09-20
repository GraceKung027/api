const express = require('express');
const app = express();
const { exec } = require('child_process');
const bodyParser = require('body-parser');
const cors = require('cors');
const knex = require('knex')({
  client: 'mysql',
  connection: {
    host: 'localhost',
    port: 3306,
    user: 'root',
    password: '',
    database: 'face_db'
  }
});

app.use(cors());
app.use(bodyParser.json()); // ใช้ bodyParser เพื่ออ่านข้อมูล JSON
const port = 7000;

// ทดสอบการทำงานของเซิร์ฟเวอร์
app.post('/', (req, res) => {
  res.send('Hello World!');
});

// ดึงรายชื่อสมาชิกทั้งหมด
app.get('/liststds', async (req, res) => {
  try {
    let rows = await knex('users');
    res.send({
      ok: 1,
      students: rows,
    });
  } catch (error) {
    res.send({ ok: 0, error: error.message });
  }
});

// ดึงข้อมูลสมาชิกตาม ID
app.get('/liststd', async (req, res) => {
  try {
    let rows = await knex('users').where({ id: req.query.id });
    res.send({
      ok: 1,
      students: rows,
    });
  } catch (error) {
    res.send({ ok: 0, error: error.message });
  }
});

// เพิ่มข้อมูลสมาชิกพร้อมกับ displayName และ dept
app.post('/register', async (req, res) => {
  const { displayName, dept } = req.body;

  // ตรวจสอบค่าที่ได้รับจากคำขอ
  if (!displayName || !dept) {
    return res.status(400).json({ error: 'Both displayName and dept are required' });
  }

  try {
    // เพิ่มข้อมูลพนักงานในตาราง staffs
    let result = await knex('staffs').insert({ displayName, dept });

    // ตรวจสอบว่าการเพิ่มข้อมูลสำเร็จ
    if (result && result[0]) {
      const staffId = result[0];  // ใช้ ID ที่ได้จากการเพิ่มข้อมูล

      // รันสคริปต์ Python เพื่อตรวจจับใบหน้าและบันทึกข้อมูลใบหน้า
      exec(`python python/register.py ${staffId}`, (error, stdout, stderr) => {
        if (error) {
          console.error(`exec error: ${error}`);
          return res.status(500).json({ error: 'Error running Python script' });
        }

        if (stderr) {
          console.error(`stderr: ${stderr}`);
          return res.status(500).json({ error: 'Python script error output' });
        }

        // เพิ่มข้อมูลในตาราง attendant
        const ts = new Date(); // สร้างตัวแปร ts สำหรับเวลา
        knex('attendant').insert({ staffId, ts })
          .then(() => {
            // สมมุติว่า stdout ของสคริปต์ Python ส่งคืนผลลัพธ์ที่ระบุว่าใบหน้าถูกบันทึกแล้ว
            console.log(`Python script output: ${stdout}`);

            // ส่งการตอบกลับเมื่อทุกอย่างสำเร็จ
            res.send({ ok: 1, message: 'Staff registered successfully and face data processed by Python script' });
          })
          .catch(err => {
            res.status(500).json({ error: 'Error inserting into attendant: ' + err.message });
          });
      });
    } else {
      return res.status(500).json({ error: 'Failed to insert staff' });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/Checkin', (req, res) => {
  exec('python python/detectfaceV.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return res.status(500).send({ ok: 0, error: 'Error running Python script' });
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
      return res.status(500).send({ ok: 0, error: 'Python script error output' });
    }
    res.send({ ok: 1, output: stdout });
  });
});

// ลบข้อมูลสมาชิก
app.post('/delete', async (req, res) => {
  const { id } = req.body;
  try {
    let ids = await knex('staffs').where({ id }).del();
    res.send({ ok: 1, id: ids });
  } catch (error) {
    res.send({ ok: 0, error: error.message });
  }
});

// อัพเดตข้อมูลสมาชิก
app.post('/update', async (req, res) => {
  const { id, displayName, dept } = req.body;
  try {
    let ids = await knex('staffs').where({ id }).update({ displayName, dept });
    res.send({ ok: 1, id: ids });
  } catch (error) {
    res.send({ ok: 0, error: error.message });
  }
});

// ตรวจสอบข้อมูลสมาชิก
app.post('/sec', async (req, res) => {
  try {
    let rows = await knex('users').where({ id: req.body.id });
    res.send({
      ok: 1,
      students: rows,
    });
  } catch (error) {
    res.send({ ok: 0, error: error.message });
  }
});

// เพิ่มการเรียกข้อมูลจากตาราง staffs
app.get('/listStaffs', async (req, res) => {
  try {
    let rows = await knex('staffs');
    res.send({
      ok: 1,
      staffs: rows,
    });
  } catch (error) {
    res.send({ ok: 0, error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
