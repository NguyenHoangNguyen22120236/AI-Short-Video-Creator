export async function deleteVideo(videoId, token) {
  try {
    const response = await fetch(
      `${process.env.REACT_APP_BACKEND_URL}/api/video/delete_video/${videoId}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      return {
        success: false,
        message: "Failed to delete video. Please try again.",
      };
    }
  } catch (error) {
    return {
      success: false,
      message: `Error deleting video: ${error.message}`,
    };
  }

  return {
    success: true,
    message: "Video deleted successfully.",
  };
}
