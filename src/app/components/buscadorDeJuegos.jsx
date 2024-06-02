"use client";
import { useState } from 'react';

const BuscarJuego = ({ juegos }) => {
  const [juegoNombre, setJuegoNombre] = useState('');
  const [resultados, setResultados] = useState([]);

  const handleSearch = (e) => {
    setJuegoNombre(e.target.value);
    if (e.target.value.length > 1) {
      const filterValue = juegos.filter((juego) =>
        juego.title.toLowerCase().includes(e.target.value.toLowerCase())
      );
      setResultados(filterValue);
    } else {
      setResultados([]);
    }
  };

  return (
    <div className="mx-20 p-3">
      <div className="mb-4 text-black">
        <input 
          type="text" 
          value={juegoNombre} 
          onChange={handleSearch} 
          placeholder="Ingresa el nombre del juego"
          className="border p-2 rounded"
        />
      </div>
      <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md">
        Buscar
      </button>
      <div className="mt-4">
      {resultados.length > 0 ? (
          <ul className="grid grid-cols-3 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {resultados.map((juego) => (
              <li key={juego.id} className="border p-4 rounded shadow-md flex flex-col items-center">
                <img src={juego.thumbnail} alt={juego.title} className="w-full h-auto mb-2"/>
                <p>{juego.title}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No se encontraron resultados.</p>
        )}
      </div>
    </div>
  );
};

export default BuscarJuego;
