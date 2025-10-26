/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  reactStrictMode: true,
  trailingSlash: false,
  outputFileTracingRoot: require("path").join(__dirname, "../../"),
};

export default nextConfig;
