const { Pool } = require('pg');

// Use environment variable for the connection string
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false, // For SSL connections (required by Render)
  },
});

// Example query to test the connection
pool.query('SELECT NOW()', (err, res) => {
  if (err) {
    console.error('Error connecting to the database', err);
  } else {
    console.log('Connected to the database:', res.rows[0]);
  }
});
