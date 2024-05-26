import { NextResponse } from "next/server";
import { query } from '@/libs/mysql';

export async function GET(req,{params}) {
  
   try {
    const result = await query('SELECT * FROM notas WHERE tarea_id=?', [params.id]);
    console.log(result)
   
    if (!result.length) {
      return NextResponse.json(
        {
          error: 'No se encontraron notas'
        }
      );
    }
    return NextResponse.json(
      result[0]
    );
  }
  catch(error) {
    console.log(error)
    return NextResponse.json(
      {
        error: 'Error al obtener notas'
      }
    );
  }}
  
export async function DELETE(req,{params}) {
  
    try {
     const result = await query('DELETE FROM notas WHERE tarea_id=?', [params.id]);
     console.log(result)
    
     if (!result.affectedRows) {
       return NextResponse.json(
         {
           error: 'No se encontraron notas'
         }
       );
     }
     return NextResponse.json(
       "torneo eliminado"
     );
   }
   catch(error) {
     console.log(error)
     return NextResponse.json(
       {
         error: 'Error al borrar notas'
       }
     );
   }}

export async function PUT(req,{params}) {
 try {
const data = await req.json()  
   const result = await query('UPDATE notas SET ? WHERE tarea_id=?', [data, params.id]);
   console.log(result)

   if (!result.affectedRows) {
     return NextResponse.json(
       {
         error: 'No se encontraron notas'
       }
     );
   }
   const updatedTorneo = await query('SELECT * from notas WHERE tarea_id = ?', [params.id])
   return NextResponse.json(
     updatedTorneo[0]
   );
 }
 catch(error) {
   console.log(error)
   return NextResponse.json(
     {
       error: 'Error al actualizar notas'
     }
   );
 }
}   