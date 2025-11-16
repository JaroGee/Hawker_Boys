import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';

type UploadTarget = {
  key: string;
  url: string;
  fields?: Record<string, string>;
};

const LOCAL_BUCKET = path.join(process.cwd(), '.uploads');

export async function ensureLocalBucket() {
  await fs.mkdir(LOCAL_BUCKET, { recursive: true });
}

export async function createLocalUploadTarget(filename: string): Promise<UploadTarget> {
  await ensureLocalBucket();
  const key = `${Date.now()}-${filename}`;
  const filepath = path.join(LOCAL_BUCKET, key);
  return { key: filepath, url: `/api/uploads/local/${key}` };
}

export function generateEncryptionKey() {
  if (!process.env.FILE_ENCRYPTION_KEY) return null;
  return Buffer.from(process.env.FILE_ENCRYPTION_KEY, 'hex');
}

export async function encryptBuffer(buffer: Buffer) {
  const key = generateEncryptionKey();
  if (!key) return buffer;
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const encrypted = Buffer.concat([cipher.update(buffer), cipher.final()]);
  const tag = cipher.getAuthTag();
  return Buffer.concat([iv, tag, encrypted]);
}
