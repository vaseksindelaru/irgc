"use client"

import { useRef, useState,useEffect } from 'react';
import axios from 'axios';
import {useRouter,useParams} from 'next/navigation'

function CrearTorneoComponent () {
  const [formData, setFormData] = useState({
    tema: '',
    subtema: '',
    descripcion: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  const form = useRef(null)
  const router = useRouter()
  const params = useParams()
  console.log(params)

  useEffect(()=>{
    if (params.id){
      axios.get('/api/torneos/'+params.id)
      .then (res => {
        console.log(res)
        setFormData({
        tema:res.data.tema,
        subtema:res.data.subtema,
        descripcion:res.data.descripcion})

      })
    }
  },[])

  const handleSubmit = async (e) => {
    e.preventDefault();

    if(!params.id){
    const res = await axios.post('/api/torneos', formData)
    console.log(res);
    }
    else{
     const res = await axios.put('/api/torneos/'+ params.id, formData)
      console.log(res)
    
    }
    router.refresh()
    form.current.reset()
    router.push('/pages/cartelera')};
 return(
        <div>
        <form ref={form} className="max-w-md mx-auto p-6 bg-gray-700 shadow-md rounded" onSubmit={handleSubmit}>
      <div className="mb-4">
        <label className="block text-gray-300 text-sm mb-2" htmlFor="tema">
          Tema
        </label>
        <input
          type="text"
          id="tema"
          name="tema"
          value={formData.tema}
          onChange={handleChange}
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>

      <div className="mb-4">
        <label className="block text-gray-300 text-sm mb-2" htmlFor="subtema">
          Subtema
        </label>
        <input
          type="text"
          id="subtema"
          name="subtema"
          value={formData.subtema}
          onChange={handleChange}
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        />
      </div>

      <div className="mb-4">
        <label className="block text-gray-300 text-sm mb-2" htmlFor="descripcion">
          Descripción
        </label>
        <textarea
          id="descripcion"
          name="descripcion"
          value={formData.descripcion}
          onChange={handleChange}
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          rows="4"
        />
      </div>

      <div className="flex items-center justify-between">
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-700 
          text-white font-bold py-2 px-4 rounded 
          focus:outline-none focus:shadow-outline">
            {params.id ? "actualisar" : "crear"}
        </button>
       
      </div>
    </form>
        </div>
    )
}
export default CrearTorneoComponent;