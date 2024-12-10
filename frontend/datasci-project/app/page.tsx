import Head from 'next/head';
import CoreFunctionalities from '../components/CoreFunctionalities';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="h-full">
      <Head>
        <title>PaperMind</title>
        <meta name="description" content="AI-powered platform for research papers" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="h-full flex flex-col">
        <section className="bg-gray-200 py-20 flex-grow flex items-center">
          <div className="container mx-auto text-center">
            <h1 className="text-5xl font-bold text-gray-800 mb-6">Welcome to PaperMind</h1>
            <p className="text-gray-600 text-xl mb-12">AI-powered predictions, recommendations, and answers for your research papers.</p>
            <Link href="/predict">
              <div className="inline-block bg-blue-600 text-white py-3 px-8 rounded hover:bg-blue-700">Get Started</div>
            </Link>
          </div>
        </section>
        <CoreFunctionalities/>
      </main>
    </div>
  );
}
