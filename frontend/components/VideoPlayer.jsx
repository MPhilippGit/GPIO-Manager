import "../scss/components/video-player.scss";

function VideoPlayer({ src, title, poster }) {
    return (
        <div className="video-player">
            {title && <h4 className="video-player__title">{title}</h4>}
            <video
                className="video-player__video"
                controls
                poster={poster}
            >
                <source src={src} type="video/mp4" />
                <source src={src} type="video/webm" />
            </video>
        </div>
    );
}

export { VideoPlayer };
