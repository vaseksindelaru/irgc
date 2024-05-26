// pages/index.js
"use client"
import React from 'react';
import axios from 'axios';

const Home = () => {
  const [imageUrl, setImageUrl] = React.useState('');

  React.useEffect(() => {
    // Solicitar la URL del gráfico al backend Flask
    const fetchImage = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/plot.png', { responseType: 'blob' });
        const imageBlob = response.data;
        const imageObjectURL = URL.createObjectURL(imageBlob);
        setImageUrl(imageObjectURL);
      } catch (error) {
        console.error('Error fetching the image', error);
      }
    };
    fetchImage();
  }, []);

  return (
    <div>
      <h1>Trading Signals and Price Direction Analysis</h1>
      {imageUrl && <img src={imageUrl} alt="Trading Signals Analysis" />}
    </div>
  );
};

export default Home;
