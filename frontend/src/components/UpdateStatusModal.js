import "../styles/UpdateStatusModal.css";
import Modal from "react-bootstrap/Modal";

export default function UpdateStatusModal({
  showUpdateModal,
  setShowUpdateModal,
  updateMessage,
}) {
  return (
    <Modal
      show={showUpdateModal}
      onHide={() => setShowUpdateModal(false)}
      centered
      dialogClassName="custom-modal"
    >
      <Modal.Header>
        <Modal.Title>Update Status</Modal.Title>
      </Modal.Header>
      <Modal.Body className="d-flex flex-column">
        {updateMessage.split("\n").map((line, idx) => (
          <div key={idx}>{line}</div>
        ))}
        <div className="d-flex justify-content-end mt-3">
          <button
            className="btn btn-primary"
            onClick={() => setShowUpdateModal(false)}
          >
            OK
          </button>
        </div>
      </Modal.Body>
    </Modal>
  );
}
