const express = require('express');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;
const flaskBackendUrl = process.env.FLASK_BACKEND_URL || 'http://localhost:5000';

app.set('view engine', 'ejs');
app.set('views', `${__dirname}/views`);

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.get('/', (req, res) => {
  res.render('index', { backendUrl: flaskBackendUrl, error: null });
});

app.post('/submit', async (req, res) => {
  try {
    const { name, email } = req.body;

    const response = await fetch(`${flaskBackendUrl}/api/students/store`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ name, email })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || 'Unable to save student');
    }

    res.redirect('/students');
  } catch (error) {
    res.status(500).render('index', {
      backendUrl: flaskBackendUrl,
      error: error.message
    });
  }
});

app.get('/students', async (req, res) => {
  try {
    const response = await fetch(`${flaskBackendUrl}/api/students`);
    const students = await response.json();

    res.render('students', { students, backendUrl: flaskBackendUrl, error: null });
  } catch (error) {
    res.status(500).render('students', {
      students: [],
      backendUrl: flaskBackendUrl,
      error: error.message
    });
  }
});

app.listen(port, () => {
  console.log(`Frontend running on port ${port}`);
});