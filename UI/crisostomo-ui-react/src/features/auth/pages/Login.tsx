// src/auth/pages/Login.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import Logo from "../../../assets/logo.png";

export const Login: React.FC = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const { login, loading, error } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const success = await login(username, password);

        if (success) {
            navigate("/"); // después tú decides a dónde
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#f3f3f3]">
            <div className="w-full max-w-sm bg-white border border-gray-300 shadow-lg p-8 rounded-md">

                {/* Logo */}
                <div className="flex flex-col items-center mb-6">
                    <img
                        src={Logo}
                        alt="Logo"
                        className="w-32 h-32 mb-2 rounded-full border-2 border-[#4d72b0]"
                    />
                    <h1 className="text-xl font-semibold text-gray-800">
                        Iniciar Sesión
                    </h1>
                </div>

                <form className="space-y-5" onSubmit={handleSubmit}>
                    <div>
                        <label className="block text-sm font-medium text-gray-700">Usuario</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="w-full mt-1 px-3 py-2 border border-gray-400 rounded-sm bg-white text-sm
                            focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-blue-600"
                            placeholder="Ingrese su usuario"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700">Contraseña</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full mt-1 px-3 py-2 border border-gray-400 rounded-sm bg-white text-sm
                            focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-blue-600"
                            placeholder="Ingrese su contraseña"
                            required
                        />
                    </div>

                    {error && (
                        <p className="text-red-600 text-sm text-center">{error}</p>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-[#4d72b0] hover:bg-[#3b5a8b] text-white py-2 text-sm font-semibold rounded-sm transition"
                    >
                        {loading ? "Validando..." : "Entrar"}
                    </button>
                </form>

                <p className="text-center text-xs mt-6 text-gray-600 hover:text-gray-800 cursor-pointer">
                    <a href="/register" className="text-[#4d72b0] hover:underline">Registrarse</a>
                </p>
            </div>
        </div>
    );
};
