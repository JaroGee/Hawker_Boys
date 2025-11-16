import { PrismaClient, Role, AnnouncementAudience, QuestStatus, SecureDocumentCategory, SecureOwnerType, ShiftStatus, ComplianceType, SupportStatus } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  await prisma.customerFeedback.deleteMany();
  await prisma.assessment.deleteMany();
  await prisma.assessmentTemplate.deleteMany();
  await prisma.questProgress.deleteMany();
  await prisma.quest.deleteMany();
  await prisma.badge.deleteMany();
  await prisma.announcement.deleteMany();
  await prisma.user.deleteMany();

  const adminPassword = await bcrypt.hash('ChangeMe123!', 10);

  const admin = await prisma.user.create({
    data: {
      email: 'admin@hawkerboys.com',
      role: Role.ADMIN,
      passwordHash: adminPassword
    }
  });

  const traineeUser = await prisma.user.create({
    data: {
      email: 'trainee@hawkerboys.com',
      role: Role.TRAINEE,
      trainee: { create: { name: 'Kai', cohort: '2024A' } }
    },
    include: { trainee: true }
  });

  const mentorUser = await prisma.user.create({
    data: {
      email: 'mentor@hawkerboys.com',
      role: Role.MENTOR,
      mentor: { create: { bio: 'Former hawker hero' } }
    }
  });

  const employerUser = await prisma.user.create({
    data: {
      email: 'employer@hawkerboys.com',
      role: Role.EMPLOYER,
      employer: { create: { companyName: 'Heritage Bites' } }
    }
  });

  const certifications = await prisma.certification.createMany({
    data: [
      { code: 'WSQ-FS1', name: 'WSQ Food Safety Level 1', level: 1 },
      { code: 'WSQ-FS2', name: 'WSQ Food Safety Level 2', level: 2 },
      { code: 'WSQ-FS3', name: 'WSQ Food Safety Level 3', level: 3 }
    ],
    skipDuplicates: true
  });

  const cert = await prisma.certification.findFirst({ where: { code: 'WSQ-FS1' } });
  if (cert) {
    await prisma.traineeCertification.create({
      data: {
        traineeId: traineeUser.trainee!.userId,
        certificationId: cert.id,
        issuedAt: new Date()
      }
    });
  }

  await prisma.announcement.createMany({
    data: [
      { title: 'New module launch', body: 'WSQ Food Safety 2 is open.', audience: AnnouncementAudience.TRAINEES, publishedAt: new Date() },
      { title: 'Mentor sync', body: 'Mentor standup on Friday.', audience: AnnouncementAudience.MENTORS, publishedAt: new Date() }
    ]
  });

  const template = await prisma.assessmentTemplate.create({
    data: {
      name: 'Stall readiness',
      criteria: [{ key: 'speed', label: 'Speed', min: 1, max: 5 }]
    }
  });

  await prisma.assessment.create({
    data: {
      traineeId: traineeUser.trainee!.userId,
      mentorId: mentorUser.id,
      templateId: template.id,
      scores: [{ key: 'speed', value: 4 }],
      notes: 'Great hustle'
    }
  });

  const quest = await prisma.quest.create({
    data: {
      title: 'Master mise en place',
      description: 'Prep station in under 10 minutes.',
      points: 50,
      startAt: new Date(),
      progress: {
        create: {
          traineeId: traineeUser.trainee!.userId,
          status: QuestStatus.ACTIVE
        }
      }
    }
  });

  const badge = await prisma.badge.create({
    data: { code: 'TEAM', title: 'Team Player', description: 'Praised by mentors', icon: '🤝' }
  });

  await prisma.traineeBadge.create({
    data: { traineeId: traineeUser.trainee!.userId, badgeId: badge.id }
  });

  await prisma.customerFeedback.create({
    data: { traineeId: traineeUser.trainee!.userId, rating: 5, comment: 'Friendly and fast!', receiptCode: 'ABC123' }
  });

  await prisma.secureDocument.create({
    data: {
      ownerType: SecureOwnerType.TRAINEE,
      traineeId: traineeUser.trainee!.userId,
      category: SecureDocumentCategory.MC,
      filename: 'mc.pdf',
      mime: 'application/pdf',
      size: 12000,
      storageKey: 'mc.pdf'
    }
  });

  await prisma.shift.create({
    data: {
      traineeId: traineeUser.trainee!.userId,
      employerId: employerUser.id,
      start: new Date(Date.now() + 86400000),
      end: new Date(Date.now() + 90000000),
      location: 'Maxwell Food Centre',
      status: ShiftStatus.CONFIRMED
    }
  });

  await prisma.complianceEvent.create({
    data: {
      traineeId: traineeUser.trainee!.userId,
      type: ComplianceType.URINE_TEST,
      start: new Date(Date.now() + 172800000)
    }
  });

  await prisma.supportTicket.create({
    data: { traineeId: traineeUser.trainee!.userId, category: 'AFTERCARE', message: 'Need meal subsidy', status: SupportStatus.OPEN }
  });

  await prisma.emergencyContact.create({
    data: { traineeId: traineeUser.trainee!.userId, name: 'Mum', relationship: 'Mother', phone: '+65 8888 2222', preferred: true }
  });

  await prisma.auditEvent.create({
    data: { actorRole: Role.ADMIN, action: 'seeded', entity: 'system', userId: admin.id }
  });
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
