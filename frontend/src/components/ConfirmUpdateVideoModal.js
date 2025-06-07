import "../styles/ConfirmUpdateVideoModal.css";
import Modal from "react-bootstrap/Modal";

export default function ConfirmUpdateVideoModal({
  showUpdateModal,
  setShowUpdateModal,
  videoTitle,
  onConfirmUpdate,
}) {
  return (
    <Modal
      show={showUpdateModal}
      onHide={() => setShowUpdateModal(false)}
      centered
      dialogClassName="custom-modal"
    >
      <Modal.Header>
        <Modal.Title>Confirm Update</Modal.Title>
      </Modal.Header>
      <Modal.Body className="d-flex flex-column">
        <p>
          Are you sure you want to update the video titled{" "}
          <strong>{videoTitle}</strong>? This action will overwrite the existing video.
        </p>
        <div className="d-flex justify-content-end mt-3">
          <button
            className="btn btn-secondary me-2"
            onClick={() => {
              setShowUpdateModal(false);
            }}
          >
            Cancel
          </button>
          <button
            className="btn btn-primary"
            onClick={onConfirmUpdate}
          >
            Update
          </button>
        </div>
      </Modal.Body>
    </Modal>
  );
}