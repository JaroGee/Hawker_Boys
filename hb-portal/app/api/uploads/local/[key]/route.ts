import { NextResponse } from 'next/server';
import fs from 'node:fs/promises';

export async function GET(_: Request, { params }: { params: { key: string } }) {
  try {
    const file = await fs.readFile(`${process.cwd()}/.uploads/${params.key}`);
    return new NextResponse(file);
  } catch (error) {
    return NextResponse.json({ message: 'Not found' }, { status: 404 });
  }
}
