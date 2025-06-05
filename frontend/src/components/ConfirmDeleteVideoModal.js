import "../styles/ConfirmDeleteVideoModal.css";
import Modal from "react-bootstrap/Modal";

export default function ConfirmDeleteVideoModal({
  showDeleteModal,
  setShowDeleteModal,
  videoTitle,
  onConfirmDelete,
  setVideoIdToDelete
}) {
  return (
    <Modal
      show={showDeleteModal}
      onHide={() => setShowDeleteModal(false)}
      centered
      dialogClassName="custom-modal"
    >
      <Modal.Header>
        <Modal.Title>Confirm Delete</Modal.Title>
      </Modal.Header>
      <Modal.Body className="d-flex flex-column">
        <p>
          Are you sure you want to delete the video titled{" "}
          <strong>{videoTitle}</strong>? This action cannot be undone.
        </p>
        <div className="d-flex justify-content-end mt-3">
          <button
            className="btn btn-secondary me-2"
            onClick={() => {
                setVideoIdToDelete(null); // Reset video ID to delete
                setShowDeleteModal(false)}
            }
          >
            Cancel
          </button>
          <button
            className="btn btn-danger"
            onClick={onConfirmDelete}
          >
            Delete
          </button>
        </div>
      </Modal.Body>
    </Modal>
  );
}