
import mysql from 'serverless-mysql';

const pool = mysql({
  config: {
    host: 'localhost', // Tu host de MySQL
    user: 'root',      // Tu usuario de MySQL
    port: 3306,        // Puerto de MySQL
    password: '21blackjack', // Tu contraseña de MySQL
    database: 'sql1'   // Tu base de datos
  }
});

export async function query(q, values) {
  try {
    const results = await pool.query(q, values);
    await pool.end();
    return results;
  } catch (e) {
    throw Error(e.message);
  }
}

export default pool;
/*
import mysql from 'mysql';

    export const config = {
      host     : 'localhost',
      user     : 'root',
      port:3306,
      password : '21blackjack',
      database : 'sql1'}

    export const pool = mysql.createConnection(config)*/