export const viteUrl = (path) => {
    const url = import.meta.env.DEV ? `http://localhost:5173${path}` : path;
    return url;
}
