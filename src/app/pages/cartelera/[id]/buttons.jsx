"use client"
import { FaTrash, FaEdit } from 'react-icons/fa';
import axios from 'axios';
import { useRouter } from 'next/navigation';

function Buttons({torneoId}) {
    const router = useRouter()
  return (
    <div className=" flex items-center mt-8 justify-between">
   
    <button
      type="button"
      className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline flex items-center"
      onClick={async ()=>{
        if (confirm('?estas seguro que quieres eliminar este torneo?'))
            {const res = await axios.delete('/api/torneos/'+ torneoId)
                if (res.status === 200){
                    router.push('/pages/cartelera')
                    router.refresh()
                }
            }
      }}
    >
      <FaTrash className="mr-2" />
      Borrar
    </button>
    <button
     onClick={() => {
        router.push(`/pages/cartelera/edit/${torneoId}`);
      }}
      type="button"
      className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline flex items-center"
    >
      <FaEdit className="mr-2" />
      Actualizar
    </button>
  </div>
  )
}

export default Buttons