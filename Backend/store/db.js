import mysql from "mysql2/promise";

const db = await mysql.createPool({
  host: "localhost",
  user: "root",
  password: "",   // default laragon: kosong
  database: "floor_eye",
});

export default db;
