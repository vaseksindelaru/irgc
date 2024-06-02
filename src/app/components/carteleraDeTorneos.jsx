import axios from 'axios'
import Link from 'next/link'

async function loadCarteleraDeTorneos() {

    const {data} = await axios.get('http://localhost:3000/api/torneos')
    return data
}

async function CarteleraDeTorneos() {
const torneos = await loadCarteleraDeTorneos()
console.log(torneos)

return (
    <div className="max-w-7xl mx-auto p-6 shadow-md rounded-lg">
      <div className="grid grid-cols-3 gap-4">
        {torneos.map((torneo) => (
          <Link key={torneo.tarea_id} className="border hover:bg-gray-500 p-4 rounded-lg shadow" href={ `/pages/cartelera/${torneo.tarea_id}`}>
          <div className="mb-2" >
              
              <div className="text-xl font-bold text-gray-300">{torneo.tarea_id}</div>
            </div>
            <div className="mb-2" >
            <div className="text-xl font-bold text-gray-300">{torneo.tema}</div>
            </div>
            <div className="mb-2">
              <div className="text-lg font-semibold text-gray-500">{torneo.subtema}</div>
            </div>
            <div>
              <div className="text-base text-white">{torneo.descripcion}</div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
  }

export default CarteleraDeTorneos