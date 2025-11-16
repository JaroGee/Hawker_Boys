import { prisma } from '../../../lib/db';
import FeedbackForm from '../../../components/public/FeedbackForm';

export default async function PublicFeedbackPage() {
  const trainees = await prisma.traineeProfile.findMany({
    select: { userId: true, name: true }
  });
  return <FeedbackForm trainees={trainees} />;
}
