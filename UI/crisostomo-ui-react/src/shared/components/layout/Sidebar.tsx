import React, { useContext } from "react";
import { Link, useLocation } from "react-router-dom";
import Logo from "../../../assets/logo.png";
import { AuthContext } from "../../../features/auth/context/AuthContext";
import { API_URL } from "../../global/globalValues";

const BookIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
    <path d="M11.25 4.533A9.707 9.707 0 0 0 6 3a9.735 9.735 0 0 0-3.25.555.75.75 0 0 0-.5.707v14.25a.75.75 0 0 0 1 .707A8.237 8.237 0 0 1 6 18.75c1.995 0 3.823.707 5.25 1.886V4.533ZM12.75 20.636A8.214 8.214 0 0 1 18 18.75c.966 0 1.89.166 2.75.47a.75.75 0 0 0 1-.708V4.262a.75.75 0 0 0-.5-.707A9.735 9.735 0 0 0 18 3a9.707 9.707 0 0 0-5.25 1.533v16.103Z" />
  </svg>
);

const UserIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" className="w-5 h-5" viewBox="0 0 24 24">
    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
  </svg>
);

const BuildingIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" className="w-5 h-5" viewBox="0 0 24 24">
    <path d="M3 22V2h18v20H3zm2-2h14V4H5v16zm2-4h2v2H7v-2zm0-4h2v2H7v-2zm4 4h2v2h-2v-2zm0-4h2v2h-2v-2zm4 4h2v2h-2v-2zm0-4h2v2h-2v-2z"/>
  </svg>
);

export const Sidebar: React.FC = () => {
  const { user } = useContext(AuthContext);
  const location = useLocation();

  const menuItems = [
    { label: "Libros", path: "/books", icon: <BookIcon /> },
    { label: "Autores", path: "/authors", icon: <UserIcon /> },
    { label: "Editorial", path: "/editorials", icon: <BuildingIcon /> },
  ];

  return (
    <aside className="w-60  border-gray-700 h-screen fixed top-0 left-0 pt-16">
      {/* Foto del usuario */}
      <div className="flex flex-col items-center mt-3">
        <img
          src={`${API_URL}/users/profile/picture/${user?.cod}/300/300`}
          className="w-40 h-40 rounded-full border shadow-sm"
          alt="Foto de perfil"
          onError={(e) => {
            e.currentTarget.onerror = null;
            e.currentTarget.src = Logo;
          }}
        />
        <span className="mt-2 font-bold text-black truncate max-w-[150px]" title={user?.full_name}>
          {user?.full_name?.toUpperCase()}
        </span>
        <small className="text-gray-700">{user?.username?.toUpperCase()}</small>
      </div>

      <hr className="border-t border-gray-700 my-4" />

      {/* Menú de navegación */}
      <div className="px-3 py-4 overflow-y-auto h-full">
        <ul className="space-y-2 text-sm font-medium">
          {menuItems.map((item) => {
            const active = location.pathname.startsWith(item.path);
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center gap-2 px-3 py-2 rounded transition-all
                    ${active
                      ? "bg-black border-l-4 border-yellow-500 text-white font-semibold"
                      : "text-gray-700 hover:bg-black hover:text-white"
                    }`}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </div>
    </aside>
  );
};
