export default function BackgroundVideo() {
    return (
        <>
            <video
                autoPlay
                muted
                loop
                playsInline
                className="
                    fixed
                    inset-0
                    h-full
                    w-full
                    object-cover
                    -z-20
                "
            >
                <source
                    src="/background.mp4"
                    type="video/mp4"
                />
            </video>

            <div
                className="
                    fixed
                    inset-0
                    bg-black/40
                    backdrop-blur-[1px]
                    -z-10
                "
            />
        </>
    );
}