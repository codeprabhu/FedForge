import type { Metadata } from "next";
import "./globals.css";

import BackgroundVideo from "@/components/layout/BackgroundVideo";
import Sidebar from "@/components/layout/Sidebar";

export const metadata: Metadata = {
    title: "FedForge",
    description: "Distributed Federated Learning Platform",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body>
                <BackgroundVideo />

                <div className="flex h-screen overflow-hidden">
                    <Sidebar />

                    <main
                        className="
                            flex-1
                            overflow-y-auto
                            p-8
                            text-stone-100
                        "
                    >
                        {children}
                    </main>
                </div>
            </body>
        </html>
    );
}