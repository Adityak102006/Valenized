export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ ok: false, error: 'Method not allowed' });
  }

  try {
    const data = req.body;
    
    // Honeypot check
    if (data._gotcha) {
      return res.status(200).json({ ok: true });
    }

    // Log the submission (visible in Vercel Dashboard -> Functions -> Logs)
    console.log('--- NEW CONTACT SUBMISSION ---');
    console.log(`Name: ${data.name}`);
    console.log(`Company: ${data.company || 'N/A'}`);
    console.log(`Email: ${data.email}`);
    console.log(`Discipline: ${data.discipline}`);
    console.log(`Budget: ${data.budget}`);
    console.log(`Brief:\n${data.brief}`);
    console.log('------------------------------');

    // NOTE: To send actual emails from Vercel, you need a service like Resend, SendGrid, or Nodemailer.
    // Since Vercel Serverless Functions can't use PHP's mail() function, the data is logged here.
    // Example using fetch for a webhook or email API could be added here.

    return res.status(200).json({ ok: true });
  } catch (error) {
    console.error('Error handling contact form:', error);
    return res.status(500).json({ ok: false, error: 'Internal Server Error' });
  }
}
