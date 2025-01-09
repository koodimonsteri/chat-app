import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import './LoginPage.css';

const validationSchema = Yup.object({
    username: Yup.string()
      .min(4, 'Username must be at least 4 characters')
      .required('Username is required'),
  
    email: Yup.string()
      .email('Invalid email format')
      .required('Email is required'),
  
    password: Yup.string()
      .min(6, 'Password must be at least 6 characters')
      .required('Password is required'),
  });


const RegisterPage = () => {
  //const [username, setUsername] = useState('');
  //const [password, setPassword] = useState('');
  //const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (values) => {
    //event.preventDefault();
    setLoading(true);
    setError('');
    setSuccess(false);

    const apiUrl = process.env.REACT_APP_API_URL;

    try {

      const requestBody = JSON.stringify({
          username: values.username,
          email: values.email,
          password: values.password,
      });
      const response = await fetch(`${apiUrl}/api/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: requestBody,
      });

      //const data = await response.json();

      if (response.ok) {
        setSuccess(true);
        // Optionally, redirect to login page after successful registration
        setTimeout(() => {
            navigate('/');
        }, 2000);
      } else {
        const errorData = await response.json();
        console.error('Registration failed:', errorData);
        alert(`Error: ${errorData.message || 'An error occurred during registration'}`);
      }
    } catch (error) {
      setError('An error occurred. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-page">
      <div className="form-container">
      <h1>Register</h1>

      <Formik
        initialValues={{ username: '', email: '', password: '' }}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting }) => (
          <Form>
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <Field
                type="text"
                id="username"
                name="username"
                placeholder="Enter username"
              />
              <ErrorMessage name="username" component="div" className="error" />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <Field
                type="email"
                id="email"
                name="email"
                placeholder="Enter email"
              />
              <ErrorMessage name="email" component="div" className="error" />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <Field
                type="password"
                id="password"
                name="password"
                placeholder="Enter password"
              />
              <ErrorMessage name="password" component="div" className="error" />
            </div>

            <button type="submit" disabled={isSubmitting}>
              Register
            </button>
          </Form>
        )}
      </Formik>

      <p>
        Already have an account? <Link to="/">Login here</Link>
      </p>
      </div>
    </div>
  );
};

export default RegisterPage;