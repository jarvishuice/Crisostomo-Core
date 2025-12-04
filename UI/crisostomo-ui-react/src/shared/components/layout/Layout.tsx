// import React from "react";
// import { Navbar } from "./Navbar";
// import { Sidebar } from "./Sidebar";
// import { Outlet } from "react-router-dom";

// export const Layout: React.FC = () => {
//     return (
//         <div className="">
//             <Sidebar />
//             <Navbar />

//             <main className="ml-60 mt-16 p-6  bg-[#f4f4f4] min-h-screen">
//                 <Outlet />
//             </main>
//         </div>
//     );
// };
import React from "react";
import { Navbar } from "./Navbar";
import { Sidebar } from "./Sidebar";
import { Outlet } from "react-router-dom";

export const Layout: React.FC = () => {
  return (
    <div className="min-h-screen flex bg-[#f4f4f4]">
      {/* Sidebar: oculto en sm, visible en md+ */}
      <aside className="hidden md:block w-60 bg-white fixed inset-y-0 left-0 z-20">
        <Sidebar />
      </aside>

      {/* Contenedor principal: ocupa todo el ancho restante */}
      <div className="flex-1 md:ml-60">
        <Navbar />
        <main className="mt-10 min-h-screen">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
