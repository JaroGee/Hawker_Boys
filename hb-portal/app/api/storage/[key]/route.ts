import { NextResponse } from 'next/server';
import { createReadStream, existsSync } from 'fs';
import { join } from 'path';

export async function GET(_: Request, { params }: { params: { key: string } }) {
  const path = join(process.cwd(), 'storage', params.key);
  if (!existsSync(path)) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }
  const stream = createReadStream(path);
  return new NextResponse(stream as any);
}
