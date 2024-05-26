
import { NextResponse } from 'next/server';
import {pool} from '@/libs/mysql'; 

export async function GET () {
  const result = await pool.query('SELECT NOW()');
  console.log (result);
  return NextResponse.json({message:result[0]['NOW()']});}
