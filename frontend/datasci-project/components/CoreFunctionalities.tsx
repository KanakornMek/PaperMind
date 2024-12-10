import Link from 'next/link';
import SearchIcon from '@mui/icons-material/Search';
import RecommendIcon from '@mui/icons-material/Recommend';
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer';
const functionalities = [
  {
    title: 'Predict',
    description: 'Predict the subject area of your research paper or text.',
    icon: SearchIcon, 
    link: '/predict',
  },
  {
    title: 'Recommend',
    description: 'Get personalized recommendations for related research papers.',
    icon: RecommendIcon,
    link: '/recommend',
  },
];

const CoreFunctionalities = () => {
  return (
    <section className="bg-gray-100 py-12">
      <div className="container mx-auto px-6">
        <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Features</h2>
        <div className="flex flex-col md:flex-row justify-between items-center space-y-8 md:space-y-0 md:space-x-8">
          {functionalities.map((func, index) => (
            <div key={index} className="bg-white shadow-md rounded-lg p-6 w-full md:w-1/2 text-center">
              <func.icon />
              <h3 className="text-xl font-semibold text-gray-800 mb-2">{func.title}</h3>
              <p className="text-gray-600 mb-4">{func.description}</p>
              <Link href={func.link}>
                <div className="inline-block bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600">
                  Try {func.title}
                </div>
              </Link>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default CoreFunctionalities;
