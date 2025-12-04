export const registerRequest = async (data: any) => {
    const response = await fetch("http://localhost:1708/users/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            accept: "application/json",
        },
        body: JSON.stringify(data),
    });

    if (response.status != 201) {
        const error = await response.text();
        throw new Error(error || "Error al registrar usuario.");
    }

    return response;
};
