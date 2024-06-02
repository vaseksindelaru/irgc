import axios from "axios"
import Buttons from "./buttons"

async function loadTorneo(torneoId){
  const {data} = await axios.get(`http://localhost:3000/api/torneos/${torneoId}`)
 return data
}

async function TorneoPage({params}) {
   const torneo = await loadTorneo(params.id)
   console.log(torneo)
  return (
    <div className="border hover:bg-gray-500 p-4 rounded-lg shadow" href={ `/pages/cartelera/${torneo.tarea_id}`}>
    <div className="mb-2" >
      <div className="text-xl font-bold text-gray-300">{torneo.tema}</div>
    </div>
    <div className="mb-2">
      <div className="text-lg font-semibold text-gray-500">{torneo.subtema}</div>
    </div>
    <div>
      <div className="text-base text-white">{torneo.descripcion}</div>
    </div>
   <Buttons torneoId={torneo.tarea_id}/>
   
  </div>
  )
}

export default TorneoPage