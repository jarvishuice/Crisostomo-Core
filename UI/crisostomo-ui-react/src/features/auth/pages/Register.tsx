import React, { useState } from "react";
import Logo from "../../../assets/logo.png";
import { useRegister } from "../hooks/useRegister";

export const Register: React.FC = () => {

    const { register, loading, error } = useRegister();

    const [form, setForm] = useState({
        cod: "",
        first_name: "",
        middle_name: "",
        last_name: "",
        second_last_name: "",
        email: "",
        date_of_birth: "",
        phone_number: "",
        username: "",
        password: "",
        confirm: "",
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (form.password !== form.confirm) {
            alert("Las contraseñas no coinciden.");
            return;
        }

        const payload = {
            cod: form.cod || "string",
            first_name: form.first_name,
            middle_name: form.middle_name || "",
            last_name: form.last_name,
            second_last_name: form.second_last_name || "",
            email: form.email,
            date_of_birth: form.date_of_birth,
            phone_number: form.phone_number || "",
            username: form.username,
            password_hash: form.password,
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
        };

        const result = await register(payload);

        if (result) {
            alert("Usuario registrado correctamente");
            window.location.href = "/login";
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#f3f3f3]">
            <div className="w-full max-w-md bg-white border border-gray-300 shadow-lg p-8 rounded-md">

                {/* Logo */}
                <div className="flex flex-col items-center mb-6">
                    <img src={Logo} alt="Logo"
                        className="rounded-full w-25 h-25 mb-2 border-2 border-[#4d72b0]" />
                    <h1 className="text-xl font-semibold text-gray-800">Crear Cuenta</h1>
                </div>

                <form className="space-y-5" onSubmit={handleSubmit}>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm">Nombre</label>
                            <input
                                name="first_name"
                                value={form.first_name}
                                onChange={handleChange}
                                className="w-full mt-1 px-3 py-2 border border-gray-400 rounded-sm"
                            />
                        </div>

                        <div>
                            <label className="block text-sm">Segundo Nombre</label>
                            <input
                                name="middle_name"
                                value={form.middle_name}
                                onChange={handleChange}
                                className="w-full mt-1 px-3 py-2 border border-gray-400 rounded-sm"
                            />
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm">Apellido</label>
                            <input
                                name="last_name"
                                value={form.last_name}
                                onChange={handleChange}
                                className="w-full mt-1 px-3 py-2 border border-gray-400 rounded-sm"
                            />
                        </div>

                        <div>
                            <label className="block text-sm">Segundo Apellido</label>
                            <input
                                name="second_last_name"
                                value={form.second_last_name}
                                onChange={handleChange}
                                className="w-full mt-1 px-3 py-2 border border-gray-400 rounded-sm"
                            />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm">Correo</label>
                        <input
                            type="email"
                            name="email"
                            value={form.email}
                            onChange={handleChange}
                            className="w-full mt-1 px-3 py-2 border border-gray-400 rounded-sm"
                        />
                    </div>

                    <div>
                        <label className="block text-sm">Fecha de nacimiento</label>
                        <input
                            type="date"
                            name="date_of_birth"
                            value={form.date_of_birth}
                            onChange={handleChange}
                            className="w-full mt-1 px-3 py-2 border border-gray-400 rounded-sm"
                        />
                    </div>

                    <div>
                        <label className="block text-sm">Usuario</label>
                        <input
                            name="username"
                            value={form.username}
                            onChange={handleChange}
                            className="w-full mt-1 px-3 py-2 border border-gray-400 rounded-sm"
                        />
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm">Contraseña</label>
                            <input
                                type="password"
                                name="password"
                                value={form.password}
                                onChange={handleChange}
                                className="w-full mt-1 px-3 py-2 border border-gray-400 rounded-sm"
                            />
                        </div>

                        <div>
                            <label className="block text-sm">Confirmar</label>
                            <input
                                type="password"
                                name="confirm"
                                value={form.confirm}
                                onChange={handleChange}
                                className="w-full mt-1 px-3 py-2 border border-gray-400 rounded-sm"
                            />
                        </div>
                    </div>

                    {error && (
                        <p className="text-red-500 text-sm text-center">{error}</p>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-[#4d72b0] hover:bg-[#3b5a8b] text-white py-2 text-sm font-semibold rounded-sm transition"
                    >
                        {loading ? "Registrando..." : "Registrar"}
                    </button>
                </form>

                <p className="text-center text-xs mt-6 text-gray-600">
                    ¿Ya tienes una cuenta?{" "}
                    <a href="/login" className="text-[#4d72b0] hover:underline">
                        Inicia sesión
                    </a>
                </p>
            </div>
        </div>
    );
};
