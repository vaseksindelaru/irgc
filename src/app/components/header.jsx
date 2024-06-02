// components/Header.js
import Link from 'next/link';

const Header = () => {
  return (
    <header className="bg-gray-900 p-4">
      <nav className="flex justify-around">
        <Link href="/pages/crearTorneo" passHref>
          <span className="text-white hover:bg-gray-700 px-3 py-2 rounded cursor-pointer" >Crear Torneo</span>
        </Link>
        <Link href="/pages/cartelera">
          <span className="text-white hover:bg-gray-700 px-3 py-2 rounded cursor-pointer">Cartelera</span>
        </Link>
        <Link href="#jugadores">
          <span className="text-white hover:bg-gray-700 px-3 py-2 rounded cursor-pointer">Jugadores</span>
        </Link>
        <Link href="#cartera">
          <span className="text-white hover:bg-gray-700 px-3 py-2 rounded cursor-pointer">Cartera</span>
        </Link>
        <Link href="#Astrobot">
          <span className="text-white hover:bg-gray-700 px-3 py-2 rounded cursor-pointer">
            
            Astrobot</span>
        </Link>
        <Link href="#info">
          <span className="text-white hover:bg-gray-700 px-3 py-2 rounded cursor-pointer">Info</span>
        </Link>
      </nav>
    </header>
  );
};

export default Header;
