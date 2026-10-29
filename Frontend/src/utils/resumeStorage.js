
const DB_NAME = "resume-analyzer-db";
const DB_VERSION = 1;
const STORE_NAME = "resumes";

function openResumeDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = () => {
      const database = request.result;

      if (!database.objectStoreNames.contains(STORE_NAME)) {
        database.createObjectStore(STORE_NAME, {
          keyPath: "id",
        });
      }
    };

    request.onsuccess = () => {
      resolve(request.result);
    };

    request.onerror = () => {
      reject(request.error || new Error("Could not open resume storage."));
    };
  });
}

function createResumeId() {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID();
  }

  return `${Date.now()}-${Math.random().toString(36).slice(2)}`;
}

export async function saveResume(file) {
  const database = await openResumeDatabase();

  const resume = {
    id: createResumeId(),
    name: file.name,
    size: file.size,
    type: file.type || "application/pdf",
    uploadedAt: new Date().toISOString(),
    file,
  };

  try {
    await new Promise((resolve, reject) => {
      const transaction = database.transaction(
        STORE_NAME,
        "readwrite"
      );

      transaction.objectStore(STORE_NAME).add(resume);

      transaction.oncomplete = () => resolve();

      transaction.onerror = () => {
        reject(
          transaction.error ||
            new Error("Could not save the resume.")
        );
      };

      transaction.onabort = () => {
        reject(
          transaction.error ||
            new Error("Saving the resume was cancelled.")
        );
      };
    });

    return resume;
  } finally {
    database.close();
  }
}

export async function getAllResumes() {
  const database = await openResumeDatabase();

  try {
    return await new Promise((resolve, reject) => {
      const transaction = database.transaction(
        STORE_NAME,
        "readonly"
      );

      const request = transaction
        .objectStore(STORE_NAME)
        .getAll();

      request.onsuccess = () => {
        const resumes = request.result || [];

        resumes.sort(
          (a, b) =>
            new Date(b.uploadedAt).getTime() -
            new Date(a.uploadedAt).getTime()
        );

        resolve(resumes);
      };

      request.onerror = () => {
        reject(
          request.error ||
            new Error("Could not load saved resumes.")
        );
      };
    });
  } finally {
    database.close();
  }
}

export async function getResumeById(id) {
  const database = await openResumeDatabase();

  try {
    return await new Promise((resolve, reject) => {
      const transaction = database.transaction(
        STORE_NAME,
        "readonly"
      );

      const request = transaction
        .objectStore(STORE_NAME)
        .get(id);

      request.onsuccess = () => {
        resolve(request.result || null);
      };

      request.onerror = () => {
        reject(
          request.error ||
            new Error("Could not open the selected resume.")
        );
      };
    });
  } finally {
    database.close();
  }
}

export async function deleteResume(id) {
  const database = await openResumeDatabase();

  try {
    await new Promise((resolve, reject) => {
      const transaction = database.transaction(
        STORE_NAME,
        "readwrite"
      );

      transaction.objectStore(STORE_NAME).delete(id);

      transaction.oncomplete = () => resolve();

      transaction.onerror = () => {
        reject(
          transaction.error ||
            new Error("Could not delete the resume.")
        );
      };

      transaction.onabort = () => {
        reject(
          transaction.error ||
            new Error("Deleting the resume was cancelled.")
        );
      };
    });
  } finally {
    database.close();
  }
}
