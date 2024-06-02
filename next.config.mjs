/** @type {import('next').NextConfig} */
const nextConfig = {
    async redirects() {
        return [
            {
                source: '/',
                destination: '/pages/cartelera',
                permanent: true,
            },
        ];
    },
};

export default nextConfig;
