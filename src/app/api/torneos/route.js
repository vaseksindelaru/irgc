import { NextResponse } from 'next/server';
import { query } from '@/libs/mysql'; // Ajusta la ruta según tu estructura de archivos

export async function GET() {
  
  const results = await query('SELECT * FROM notas');
  
  return NextResponse.json(
    results
  );
}


export async function POST(request) {
  try {
    const { tema, subtema, descripcion } = await request.json();
    
    const result = await query(
      'INSERT INTO notas (tema, subtema, descripcion) VALUES (?, ?, ?)', 
      [tema, subtema, descripcion]
    );
    
    console.log(result);  

    return NextResponse.json({ message: 'Torneo creado exitosamente' });
  } catch (error) {
    console.error('Error creando el torneo:', error);
    return NextResponse.error(new Error('Error interno del servidor'));
  }
}

/*
import { NextResponse } from "next/server";
import {pool} from "@/libs/mysql";
export function GET() {
  return NextResponse.json(
    "obteniendo torneos",
  );
}

export async function POST(request) {
    const {tema,subtema,descripcion} = await request.json()
   
    
    const result = await pool.query("INSERT INTO notas SET ?", 
    {tema:tema,subtema:subtema,descripcion:descripcion}); 
    console.log(result)  
   
    return NextResponse.json("creando torneo");
  }*/